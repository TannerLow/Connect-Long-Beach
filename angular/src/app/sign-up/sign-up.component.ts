import { Component, OnInit } from '@angular/core';
import {NgForm} from "@angular/forms";
import { RegistrationInfo } from '../api-objects/RegistrationInfo';
import { RegistrationResponse } from '../api-objects/RegistrationResponse';
import { DatabaseService } from '../database.service';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

  emailPattern = "^[a-z0-9._-]+@student\.csulb\.edu$";
  passPattern = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&]).{8,20}";

  constructor(private database: DatabaseService) { }

  ngOnInit(): void {
  }

  onInfoItem(form: NgForm){
    const value = form.value;
    console.log(value);

    let password = this.database.hashPassword(value.passwordFieldName);

    let info: RegistrationInfo = {
        firstName: value.fname,
        lastName:value.lname,
        gender: value.gender,
        email: value.email,
        password: password,
        month: value.month,
        day: value.day,
        year: value.year
    }

    this.database.register(info).subscribe((data: RegistrationResponse) => {
        console.log("Restration response: " + data.response);
        if (data.response) {
            console.log("Registered successfully");
        }
        else {
            console.log("Failed Registration")
        }
    });
  }
}
