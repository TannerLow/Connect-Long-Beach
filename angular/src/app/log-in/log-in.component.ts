import { Component, OnInit } from '@angular/core';
import {NgForm} from "@angular/forms";
import { Router } from '@angular/router';
import { LoginCredentials } from '../api-objects/LoginCredentials';
import { LoginResponse } from '../api-objects/LoginResponse';
import { DatabaseService } from '../database.service';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {

    emailPattern = "^[a-z0-9._-]+@student\.csulb\.edu$";

    static loggedIn = false;
    static userID = -1;

    constructor(private router: Router, private database: DatabaseService) { }

    ngOnInit(): void {

    }

    // attempt login with Credentials from login form
    // TAKES USER TO SIGN UP PAGE AS PLACEHOLDER
    onInfoItem(form: NgForm){
        const value = form.value;
        console.log(value);
        let password = this.database.hashPassword(value.password);
        let credentials: LoginCredentials = {email: value.emailAddress, password: password};
        console.log(credentials);
        this.database.login(credentials).subscribe((data: LoginResponse) => {
            console.log("Login response: " + data.response);
            LogInComponent.userID = data.userID;
            LogInComponent.loggedIn = true;
            if(data.response) {
                this.router.navigate(['/sign-up']);
            }
        });
    }
}
