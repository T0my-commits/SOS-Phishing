import { useFetch, useCookie, useRuntimeConfig, useNuxtApp } from '#app';

export const useApiRequest = async (url, options = {}) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 7000);
  const { $toast } = useNuxtApp();

  try {
    const { data, error } = await useFetch(url, {
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      headers: {
        Authorization: `Bearer ${useCookie('access_token').value}`,
        ...(options.headers || {}),
      },
      signal: controller.signal,
      ...options,
    });

    if (error.value) {
      if (error.value.name === 'AbortError') {
        $toast.add({
          severity: 'warn',
          summary: 'Request timed out',
          position: 'top-center',
          life: 5000,
        });
      } else {
        $toast.add({
          severity: 'error',
          summary: 'Error fetching data',
          position: 'top-center',
          life: 5000,
        });
      }
      return null;
    }

    return data.value;
  } catch (e) {
    $toast.add({
      severity: 'error',
      summary: 'Unexpected error',
      position: 'top-center',
      life: 5000,
    });
    console.error('Unexpected error:', e);
    return null;
  } finally {
    clearTimeout(timeoutId);
  }
};
