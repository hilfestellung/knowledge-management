import {createReducer, on} from "@ngrx/store";
import {AuthenticationState, initialAuthenticationState} from "./state";
import {login, loginFailure, loginSuccess, logout} from "./actions";


const reducer = createReducer(initialAuthenticationState,
  on(login, (state: AuthenticationState, {username}) => ({...state, isPending: true, error: undefined})),
  on(loginSuccess, (state: AuthenticationState, {user}) => ({...state, isPending: false, isAuthenticated: true, user, error: undefined})),
  on(loginFailure, (state: AuthenticationState, {error}) => ({...state, isPending: false, error})),
  on(logout, (state: AuthenticationState) => ({...state, isPending: false, isAuthenticated: false, user: undefined, error: undefined}))
);

export default reducer;
