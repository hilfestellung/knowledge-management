import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {AuthenticationService} from "./services/authentication.service";

import {ProfileComponent} from "./profile/profile.component";

const routes: Routes = [
    {path: 'authentication', component: ProfileComponent},
  ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [AuthenticationService]
})
export class AuthenticationRoutingModule {
}
