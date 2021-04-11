export const AUTHENTICATION_STATE_NAME = 'authentication';

export interface AuthenticationState {
  isAuthenticated: boolean;
  isPending: boolean,
  user?: any,
  error?: Error
}

export const initialAuthenticationState: AuthenticationState = {
  isAuthenticated: false,
  isPending: false,
}
