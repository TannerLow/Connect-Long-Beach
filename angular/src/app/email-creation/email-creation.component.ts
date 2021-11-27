import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-email-creation',
  templateUrl: './email-creation.component.html',
  styleUrls: ['./email-creation.component.css']
})
export class EmailCreationComponent implements OnInit {

  activationCode: string = ""
  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  submit(): void{
  //if click on submit. we need to make sure that the value is the same as the one that was sent to the user email
  //  retrieve such value from database and compare it here if so ... it will be send to the log in page again
    console.log(this.activationCode)
    this.router.navigateByUrl('log-in')
  }

}
