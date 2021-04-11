import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {StoreModule} from "@ngrx/store";
import {HttpClientModule} from "@angular/common/http";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {FlexModule} from "@angular/flex-layout";
import {MatButtonModule} from "@angular/material/button";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {FormsModule} from "@angular/forms";
import {MatDialogModule} from "@angular/material/dialog";

import reducer from "./redux/reducer";
import {AUTHENTICATION_STATE_NAME} from "./redux/state";

import {AuthenticationRoutingModule} from './authentication-routing.module';
import {AuthenticationService} from "./services/authentication.service";
import {LoginDialogComponent} from './login/login-dialog.component';
import {LoginDialogContentComponent} from './login/login-dialog-content.component';
import {ProfileComponent} from './profile/profile.component';
import {MatSlideToggleModule} from "@angular/material/slide-toggle";


@NgModule({
  declarations: [LoginDialogComponent, ProfileComponent, LoginDialogContentComponent],
  imports: [
    AuthenticationRoutingModule,
    CommonModule,
    HttpClientModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    MatSlideToggleModule,
    StoreModule.forFeature(AUTHENTICATION_STATE_NAME, reducer),
    FlexModule,
    FormsModule
  ],
  providers: [AuthenticationService],
  exports: [LoginDialogComponent]
})
export class AuthenticationModule {
}
