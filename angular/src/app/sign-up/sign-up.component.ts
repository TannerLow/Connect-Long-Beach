import { Component, OnInit } from '@angular/core';
import {NgForm} from "@angular/forms";


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

  emailPattern = "^[a-z0-9._-]+@student\.csulb\.edu$";
  passPattern = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&]).{8,20}";

  constructor() { }

  onInfoItem(form: NgForm){
    const value = form.value;
    console.log(value);
  }

  ngOnInit(): void {
  }

}
