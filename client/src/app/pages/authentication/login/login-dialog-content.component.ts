import {Component, OnInit} from '@angular/core';
import {AuthenticationService} from "../services/authentication.service";
import {suppressDefaultBehaviour} from "../../../shared/utils";

@Component({
  selector: 'app-login',
  templateUrl: './login-dialog-content.component.html',
  styleUrls: ['./login-dialog-content.component.sass']
})
export class LoginDialogContentComponent implements OnInit {

  username: string = '';
  password: string = '';
  rememberMe: boolean = false;

  constructor(public authentication: AuthenticationService) {
  }

  ngOnInit(): void {
    this.rememberMe = Boolean(localStorage.getItem('remember_me'));
    if (this.rememberMe) {
      this.username = localStorage.getItem('username') || '';
    }
  }

  onUsernameChange({target}: any) {
    this.username = target.value;
  }

  onPasswordChange({target}: any) {
    this.password = target.value;
  }

  onSubmit(event: Event): void {
    suppressDefaultBehaviour(event);
    if (this.rememberMe) {
      localStorage.setItem('username', this.username);
      localStorage.setItem('remember_me', 'true');
    } else {
      localStorage.removeItem('username');
      localStorage.removeItem('remember_me');
    }
    this.authentication.login(this.username, this.password);
  }
}
