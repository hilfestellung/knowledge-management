import {createSelector} from "@ngrx/store";

import {AUTHENTICATION_STATE_NAME, AuthenticationState} from "./state";

function selectAuthentication(state: any): AuthenticationState {
  return state[AUTHENTICATION_STATE_NAME];
}
const isAuthenticated = createSelector(selectAuthentication, state => state.isAuthenticated);
const isPending = createSelector(selectAuthentication, state => state.isPending);
const user = createSelector(selectAuthentication, state => state.user);
const error = createSelector(selectAuthentication, state => state.error);
const hasError = createSelector(selectAuthentication, state => !!state.error);

export const authenticationSelectors = {
  isAuthenticated,
  isPending,
  user,
  error,
  hasError
};
