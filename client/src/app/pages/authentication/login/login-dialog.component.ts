import {Component, OnDestroy, OnInit} from '@angular/core';
import {MatDialog, MatDialogRef} from "@angular/material/dialog";

import {AuthenticationService} from "../services/authentication.service";
import {LoginDialogContentComponent} from "./login-dialog-content.component";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-login',
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.sass']
})
export class LoginDialogComponent implements OnInit, OnDestroy {

  private authenticatedSubscription?: Subscription;
  private loginDialog?: MatDialogRef<any>;

  constructor(public authenticationService: AuthenticationService, private dialog: MatDialog) {
  }

  ngOnInit(): void {
    this.authenticationService.isAuthenticated.subscribe(isAuthenticated => {
      if (this.loginDialog != null) {
        this.loginDialog.close();
      }
    })
  }

  ngOnDestroy() {
    if (this.authenticatedSubscription) {
      this.authenticatedSubscription.unsubscribe();
    }
  }

  openDialog() {
    this.loginDialog = this.dialog.open(LoginDialogContentComponent);
  }
}
