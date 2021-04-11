import {AUTHENTICATION_STATE_NAME, AuthenticationState} from "../../pages/authentication/redux/state";

export default interface AppState {
  [AUTHENTICATION_STATE_NAME]: AuthenticationState
}
