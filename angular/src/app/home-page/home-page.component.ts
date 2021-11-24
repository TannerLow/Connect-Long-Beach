import { Component, NgModule, OnInit } from '@angular/core';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {
  postText = "Here is a picture of the Walter Pyramid at the University of Long Beach."
  privacy = "Public"
  currentDate = "Nov 10 2021, 2:00pm" 
  likes = "12"
  constructor() { }

  ngOnInit(): void {
      
  }

}
