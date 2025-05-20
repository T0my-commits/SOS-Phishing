import { isAuthenticated } from '@/composables/useAuth';
import { debugPrint } from '@/assets/js/debug';

export default defineNuxtRouteMiddleware(async (to, from) => {
  debugPrint("/app/middlewares/auth.ts", "Checking user authentication");

  // check if user is authenticated
  if (await isAuthenticated(2) !== 0) {
    debugPrint("/app/middlewares/auth.ts", "User not authenticated. Redirect to /login");
    return navigateTo('/login')
  }

  debugPrint("/app/middlewares/auth.ts", "User authenticated");
})
