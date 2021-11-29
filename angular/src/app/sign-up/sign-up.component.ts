import { Component, Inject, NgModule, OnInit } from '@angular/core';
import {NgForm} from "@angular/forms";
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { RegistrationInfo } from '../api-objects/RegistrationInfo';
import { RegistrationResponse } from '../api-objects/RegistrationResponse';
import { DatabaseService } from '../database.service';
import { DialogData } from '../profile/profile.component';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

  emailPattern = "^[a-z0-9._-]+@student\.csulb\.edu$";
  passPattern = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&]).{8,20}";

  emailAdd = "";

  userCode = "";
  codeValidated = false;

  constructor(public dialog: MatDialog, private database: DatabaseService, private router: Router) { }

  ngOnInit(): void {
  }

  onInfoItem(form: NgForm){
    const value = form.value;
    //console.log(value);

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
            this.router.navigate(['/log-in']);
        }
        else {
            console.log("Failed Registration")
        }
    });
  }

  openDialog(form: NgForm): void {
    const dialogRef = this.dialog.open(EmailVerificationDialog, {
      width: '30%',
      data: {email: this.emailAdd}
    });

    //once the dialog closes.. the elements get saved into the result and then assign each value accordingly
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      console.log(result)
      if(result !== undefined) {
        this.userCode = result[0];
        console.log(this.userCode);
        this.onInfoItem(form);
      }
    });
  }
}

@Component({
    selector: 'email-verification-dialog',
    templateUrl: './email-verification-dialog.component.html',
    styleUrls: ['./email-verification-dialog.component.css']
})
export class EmailVerificationDialog implements OnInit{
    code = "Default Code";
    correct = "Hello World";
  
    //data from interface DailogData is injected into the Dialog (the component that pops out)
    constructor(
        private databaseService: DatabaseService,
        public dialogRef: MatDialogRef<EmailVerificationDialog>,
        @Inject(MAT_DIALOG_DATA) private data: any) {}
  
    //inherits libraries from app root
    ngOnInit(): void {
        this.code = ""
        this.correct = this.generateCode();
        this.databaseService.sendCode(this.data.email, this.correct).subscribe();
    }

    generateCode(): string {
        let r = (Math.random() + 1).toString(36).substring(7);
        console.log("Verification code: ", r);
        return r;
    }
}