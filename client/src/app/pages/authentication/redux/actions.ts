import {createAction} from "@ngrx/store";

export const login = createAction('[Authentication] Login', (username: string, password: string) => ({
  username, password
}));
export const loginSuccess = createAction('[Authentication] Login success', user => ({user}));
export const loginFailure = createAction('[Authentication] Login failure', error => ({error}));
export const logout = createAction('[Authentication] Logout');
