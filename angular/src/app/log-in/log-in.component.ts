import { Component, OnInit } from '@angular/core';
import {NgForm} from "@angular/forms";

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {

  emailPattern = "^[a-z0-9._-]+@student\.csulb\.edu$";

  constructor() { }

  onInfoItem(form: NgForm){
    const value = form.value;
    console.log(value);
  }
  ngOnInit(): void {
  }

}
