import { useRouter } from '#app';
import { useCookie } from '#app';
import { useFetch } from '#app';
import { useToast } from 'primevue/usetoast';
import { debugPrint } from '@/assets/js/debug';


/**
 * Login function with access token creation cookie
 * @param {string} username - Username provided by the user
 * @param {string} password - Password provided by the user
 * @param {boolean} rememberMe - Whether the user wants to be remembered
 * @returns {void}
 */
export async function loginUser(username, password, rememberMe) {
  debugPrint("loginUser", "Start function loginUser");

  const router = useRouter()
  const error = ref('')
  const { $toast } = useNuxtApp()
  debugPrint("loginUser", "Import toast: " + $toast);
  
  try {
    debugPrint("loginUser", "Start fetch API");
    const data = await $fetch('/api/token/', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      credentials: 'include',
      body: { 'username': username, 'password': password },
    })
    debugPrint("loginUser", "Collecting API results");

    const access = data?.access
    const refresh = data?.refresh
    debugPrint("loginUser", "End of getting values from response");

    if (access && refresh) {
      debugPrint("loginUser", "Good credentials");
      useCookie('access_token').value = access
      useCookie('refresh_token').value = refresh

      $toast.add({ severity: 'success', summary: 'Login Successful', detail: 'Welcome back!', position: 'top-center', life: 5000 });
      router.push('/')
    } else {
      debugPrint("loginUser", "Missing tokens");
      error.value = 'Error: missing tokens'
      $toast.add({ severity: 'error', summary: 'Login Failed', detail: 'Invalid server response.', position: 'top-center', life: 5000 });
    }
  } catch (e) {
    debugPrint("loginUser", "Exception caught: Error during login process: " + e);
    error.value = 'Connection error to server'
    $toast.add({ severity: 'error', summary: 'Server Error', detail: 'Could not connect to server.', position: 'top-center', life: 5000 });
  }
}

/**
 * Logout function to clear cookies and redirect to login page
 * @returns {void}
 */
export async function logoutUser(isToast = false) {
  debugPrint("logoutUser", "Start function logoutUser");

  const router = useRouter();
  const { $toast } = useNuxtApp();

  // Remove tokens from cookies
  useCookie('access_token').value = null;
  useCookie('refresh_token').value = null;
  
  // Redirect to login page
  debugPrint("logoutUser", "Logout user redirect");
  if (isToast) {
    $toast.add({ severity: 'success', summary: 'Logout Successful', position: 'top-center', life: 5000 });
  }
  router.push('/');
}

/**
 * Check if the user is authenticated by checking the access token
 * @returns {int} - 0 if success, 1 if redirect to /login page, 2 elsewise
 */
export async function isAuthenticated(retryNumber = 1) {
  debugPrint("isAuthenticated", "Start function isAuthenticated");

  const { $toast } = useNuxtApp()
  const router = useRouter()
  let authNeedRetry = false;
  let authNeedRefresh = false;
  let authNeedLogin = false;
  const accessToken = useCookie('access_token').value

  if (accessToken !== undefined && accessToken !== '') {
    debugPrint("isAuthenticated", "Retrieved access token: " + accessToken.substring(0, 30) + "...");
    try {
      // Fetch the user's profile from the server using the access token
      debugPrint("isAuthenticated", "Request backend for verification");
      const { data, error } = await $fetch('/api/token/verify/', {
        method: 'POST',
        baseURL: useRuntimeConfig().public.apiBaseUrl,
        body: { 'token': accessToken },
      })

      // manage errors
      if (error && error.value) {
        debugPrint("isAuthenticated", "Error verifying token: " + error.value);
        authNeedRetry = true;
      // manage JWT codes status
      } else if (data && data.value?.code === 'token_not_valid') {
        debugPrint("isAuthenticated", "Token not valid");
        authNeedRefresh = true;
      // if everything OK
      } else {
        debugPrint("isAuthenticated", "Token verified");
        return 0;
      }
    } catch (e) {
      // if token invalid
      if (e.message.includes('401 Unauthorized')) {
        debugPrint("isAuthenticated", "Error: Token expired or invalid");
        authNeedRefresh = true;
      // other cases
      } else {
        debugPrint("isAuthenticated", "Exception caught: Error during token verification process: " + e);
        authNeedRetry = true;
      }
    }
  } else {
    debugPrint("isAuthenticated", "No token founded");
    authNeedLogin = true;
  };

  // retry authentication
  if (authNeedRetry) {
    if (retryNumber > 0) {
      debugPrint("isAuthenticated", "Try new attempt: " + retryNumber + " left");
      return isAuthenticated(retryNumber - 1);
    } else {
      debugPrint("isAuthenticated", "No connection attemps left, abort");
      authNeedRefresh = true;
    }
  };
  // try refresh access token
  if (authNeedRefresh) {
    debugPrint("isAuthenticated", "Try to refresh token");
    if (await refreshAccessToken() === 0) {
      debugPrint("isAuthenticated", "access token refreshed");
      return 0;
    } else {
      debugPrint("isAuthenticated", "Refresh access token failed. Forcing user relogin");
      authNeedLogin = true;
    }
  };
  // user must login
  if (authNeedLogin) {
    logoutUser();
    debugPrint("isAuthenticated", "Redirect to /login");
    $toast.add({ severity: 'warn', summary: 'User not connected', position: 'top-center', life: 5000 });
    router.push('/login');
    return 1;
  };

  return 2;
}

/**
 * Get the current user's profile from the server
 * @returns {Object|null} - The user profile or null if not authenticated
 */
export async function getUserProfile() {
  debugPrint("getUserProfile", "Start function getUserProfile");

  const router = useRouter();
  const accessToken = useCookie('access_token').value

  debugPrint("getUserProfile", "Check access_token cookie");
  if (accessToken === undefined || accessToken === '') {
    debugPrint("getUserProfile", "User not authenticated");
    return null;
  }

  debugPrint("getUserProfile", "access_token cookie exists and have value " + accessToken.substring(0, 30) + "...");

  try {
    // Fetch the user's profile from the server using the access token
    debugPrint("getUserProfile", "Request backend server for profile");
    const { data, error } = await useFetch('/api/user/me/', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }).catch(err => {
      debugPrint("getUserProfile", "useFetch error: " + err);
    });

    debugPrint("getUserProfile", "Request finished: " + data.value);

    if (error && error.value) {
      debugPrint("getUserProfile", "Error fetching user profile: " + error.value);
      return null;
    }

    if (data.value) {
      debugPrint("getUserProfile", "User profile fetched");
      return data.value || null;
    }
  } catch (e) {
    debugPrint("getUserProfile", "Exception caught: Error fetching user profile: " + e);
    return null;
  }
}

/**
 * Refresh the access token using the refresh token
 * @returns {int} 0 if success, 1 if not token founded, 2 if error with request, 3 otherwise
 */
export async function refreshAccessToken() {
  debugPrint("refreshAccessToken", "Start function refreshAccessToken");

  const refreshToken = useCookie('refresh_token').value
  const { $toast } = useNuxtApp()

  if (!refreshToken) {
    debugPrint("refreshAccessToken", "No refresh token found");
    return 1
  }

  debugPrint("refreshAccessToken", "Send request to refresh token");

  try {
    // Send the refresh token to the backend to get a new access token
    const { data, error } = await useFetch('/api/token/refresh/', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      body: { refresh: refreshToken },
    }).catch(err => {
      debugPrint("refreshAccessToken", "useFetch error: " + err);
    });

    if (error && error.value) {
      debugPrint("refreshAccessToken", "Error refreshing access token: " + error.value);
      return 2
    }

    const newAccessToken = data.value?.access
    const newRefreshToken = data.value?.refresh
    debugPrint("refreshAccessToken", "Get new acces token value: " + newAccessToken.substring(0, 30) + "...");
    debugPrint("refreshAccessToken", "Get new refresh token value: " + newRefreshToken.substring(0, 30) + "...");
    if (newAccessToken && newRefreshToken) {
      debugPrint("refreshAccessToken", "Set new access and refresh token into cookies");
      $toast.add({ severity: 'info', summary: 'Access token renewed!', position: 'top-center', life: 5000 });
      useCookie('access_token').value = newAccessToken;
      useCookie('refresh_token').value = newRefreshToken;
      return 0
    }
  } catch (e) {
    debugPrint("refreshAccessToken", "Exception caught: Error during token refresh process: " + e);
    return 3
  }
}
