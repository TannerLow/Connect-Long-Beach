import { Component, NgModule, OnInit } from '@angular/core';


@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {

  static signalBackActivate: string = 'block'
  constructor() { }

  ngOnInit(): void {
  }

}


