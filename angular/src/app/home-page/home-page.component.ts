import { Component, NgModule, OnInit } from '@angular/core';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {
  firstName = "CONNECT LONG"
  lastName = "BEACH"
  postText = "Here is a picture of the Walter Pyramid at the University of Long Beach."
  privacy = "Public"
  currentDate = "Nov 10 2021, 2:00pm" 
  likes = "12"

  uploadedFile? = "";

  constructor() { }
  
  ngOnInit(): void {
  }

//   onFileSelected(event){ //takes element(file) and 
//     this.uploadedFile = event.target.files[0];
//     console.log(this.uploadedFile);
//   }
  onFileSelected(event){
    const files = event.target.files;
    const reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
        console.log(reader.result?.toString());
        this.uploadedFile = reader.result?.toString();
    }
  }
  onUpload()//function will upload file onto database when post is clicked 
  {
  }

}
