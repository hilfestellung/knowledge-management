import {Injectable} from '@angular/core';
import {Store} from "@ngrx/store";
import {Observable, of} from "rxjs";
import {authenticationSelectors} from "../redux/selectors";
import {tap} from "rxjs/operators";
import {login, logout} from "../redux/actions";

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  isAuthenticated: Observable<boolean>;
  isPending: Observable<boolean>;
  error: Observable<Error | undefined>;
  hasError: Observable<boolean>;

  constructor(private store: Store<any>) {
    this.isAuthenticated = store.select(authenticationSelectors.isAuthenticated);
    this.isPending = store.select(authenticationSelectors.isPending);
    this.error = store.select(authenticationSelectors.error);
    this.hasError = store.select(authenticationSelectors.hasError);
  }

  login(username: string, password: string) {
    this.store.dispatch(login(username, password))
  }

  logout() {
    this.store.dispatch(logout())
  }
}
