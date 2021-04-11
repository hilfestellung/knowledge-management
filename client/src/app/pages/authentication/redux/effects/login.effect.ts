import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";

import {of} from "rxjs";
import {catchError, map, mergeMap} from "rxjs/operators";
import jwtDecode, {JwtPayload} from 'jwt-decode';

import {Actions, createEffect, ofType, ROOT_EFFECTS_INIT} from "@ngrx/effects";

import {login, loginFailure, loginSuccess, logout} from "../actions";

const PUBLIC_KEY = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqqAIialz3FXFYJ2XdDZU
tlYWTRmBY2F2M0mbpnp5mGdkOZdV9E2vdCCFq5wCzXQslU86WqPEbe1Ez75p54/c
wodIq7CoYrop0XjnyNRkpbOL/ucBEQnRQg23HS55MDbtVIwZICGZ2ESDULQ6gHVn
woq4eYZSpmgl4+ZtQoUiFLYySz/OicPj9JcgOzAOtKlAz9wMOa+cdB3uKJHEoslz
DxRsNKSATKYXtikpf4ERXTi1zQlRmXeEubM20zYQdnL6aFm0pjOPoHXRhF9ZhXDM
0zIlQ/o8vF2wEubdaC/9WA+yyImgj73CknnY/A6/cgJVzS75mx2tBdJGq/It2YSm
iwIDAQAB
-----END PUBLIC KEY-----
`;

const headers = new HttpHeaders({
  'Content-Type': 'application/json'
});

@Injectable()
export class LoginEffect {

  init$ = createEffect(() => this.actions$.pipe(
    ofType(ROOT_EFFECTS_INIT),
    mergeMap(() => {
      const token = localStorage.getItem('access_token');
      const expiresValue = localStorage.getItem('expires');
      console.log(expiresValue, token)
      if (token == null || expiresValue == null) {
        return of(loginFailure(undefined));
      }
      const expires = parseInt(expiresValue, 10);
      if (expires < Date.now()) {
        return of(loginFailure(undefined));
      }
      const decoded = jwtDecode<JwtPayload>(token, {header: false});
      return this.http.get('/api/user', {
        headers: new HttpHeaders({
          'Authorization': 'Bearer ' + token
        })
      }).pipe(
        map(response => loginSuccess({...response, permissions: (decoded as any).permissions})),
        catchError(response => of(loginFailure(response.error)))
      );
    })
  ));

  login$ = createEffect(() => this.actions$.pipe(
    ofType(login),
    mergeMap(({username, password}) => {
      return this.http.put('/api/user/login', {username, password}, {headers}).pipe(
        mergeMap((response: any) => {
          localStorage.setItem('access_token', response.token);
          localStorage.setItem('expires', (response.expires * 1000).toString());
          const decoded = jwtDecode<JwtPayload>(response.token, {header: false});
          return this.http.get('/api/user', {
            headers: new HttpHeaders({
              'Authorization': 'Bearer ' + response.token
            })
          }).pipe(
            map(response => loginSuccess({...response, permissions: (decoded as any).permissions})),
            catchError(err => of(loginFailure(err)))
          );
        }),
        catchError(response => of(loginFailure(response.error)))
      )
    })
    )
  );

  logout$ = createEffect(() => this.actions$.pipe(
    ofType(logout),
    map(action => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('expires');
    })
  ), {
    dispatch: false
  })

  constructor(
    private actions$: Actions,
    private http: HttpClient
  ) {
  }
}
