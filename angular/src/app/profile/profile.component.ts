import {Component, Inject, OnInit} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { ProfileData } from '../api-objects/ProfileData';
import { ProfileUpdateData } from '../api-objects/ProfileUpdateData';
import { DatabaseService } from '../database.service';
import { LogInComponent } from '../log-in/log-in.component';
import { ImageResponse } from '../api-objects/ImageResponse';
import { StoreImageResponse } from '../api-objects/StoreImageResponse';
//Data used for the Dialog data.. might want to export this interface to save space
export interface DialogData {
  firstName: string;
  lastName: string;
  major: string;
  year: string;
  selectedGender: string;
  interest: string [];
  selectedCourses: string [];
  pa: any;
  background: any;
}


@Component({
  selector: 'profile-component',
  templateUrl: 'profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements  OnInit{
  //firstName, lastName, should be defeault since we are getting it from the database
  firstName = "Default"
  lastName = "Name"
  major = ""
  year = ""
  selectedGender =  ""
  interest: string[] = [];
  selectedCourses: string[] = [];
  //default values for the image since the profile hasnt been assigned images
  background = "/static/assets/Walter_Pyramid.jpg"
  backgroundFile = "";
  pa = "/static/assets/anonymous.png"
  paFile = "";

  
  //biography variables
  biography: any = "";
  signalContent: boolean = true;

  constructor(public dialog: MatDialog, private databaseService: DatabaseService) {}

    ngOnInit(): void {
        // Retrieve user's details
        let pathURL = LogInComponent.pathURL;
        let userID = LogInComponent.userID;
        if(pathURL !== "null") {
            this.databaseService.getProfile(userID, pathURL).subscribe((data: ProfileData) => {
                console.log(data);
                this.year = data.grade.toString();
                this.biography = data.about;
                this.selectedGender = data.gender;
                this.interest = data.interests;
                this.selectedCourses = data.courses;
                this.firstName = data.firstName;
                this.lastName = data.lastName;
                this.major = data.major;
                this.backgroundFile = data.coverPic;
                this.paFile = data.profilePic;
                // if they have a custom bg pic retrieve it
                if(this.backgroundFile !== this.background) {
                    this.databaseService.getImage(this.backgroundFile).subscribe((data: ImageResponse) => {
                        if(data.retrieved) {
                            this.background = data.image;
                        }
                    });
                }
                // if they have a custom profile pic retrieve it
                if(this.paFile !== this.pa) {
                    this.databaseService.getImage(this.paFile).subscribe((data: ImageResponse) => {
                        if(data.retrieved) {
                            this.pa = data.image;
                        }
                    });
                }
            });
        }
        else{
            console.error("Error retrieving profile data. See ngOnInit() in ProfileComponent.");
        }
    }

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '25%',
      data: {firstName: this.firstName, lastName: this.lastName,major: this.major, year: this.year, selectedGender: this.selectedGender, interest: this.interest, selectedCourses: this.selectedCourses, pa: this.pa, background: this.background}
    });

    //once the dialog closes.. the elements get saved into the result and then assign each value accordingly
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      console.log(result)
      if(result !== undefined) {
        this.firstName = result[0];
        this.lastName = result[1];
        this.major = result[2];
        this.year = result[3];
        this.selectedGender = result[4];
        this.interest = result[5];
        this.selectedCourses = result[6];
        this.pa = result[7];
        this.background = result[8];
        console.log(this.firstName);
        console.log(this.lastName);
        console.log(this.major);
        console.log(this.year);
        console.log(this.selectedGender);
        console.log(this.interest);
        console.log(this.selectedCourses);

        // if either picture has changed then store it in the database
        if(this.pa !== this.paFile){
            this.databaseService.storeImage(this.pa, this.paFile).subscribe((data: StoreImageResponse) => {
                this.paFile = data.path;
                if(this.background !== this.backgroundFile){
                    this.databaseService.storeImage(this.background, this.backgroundFile).subscribe((data: StoreImageResponse) => {
                        this.backgroundFile = data.path;
                        this.persistProfileData();
                    });
                }
                else{
                    this.persistProfileData();
                }
            });
        }
        else if(this.background !== this.backgroundFile){
            this.databaseService.storeImage(this.background, this.backgroundFile).subscribe((data: StoreImageResponse) => {
                this.backgroundFile = data.path;
                this.persistProfileData();
            });
        }
      }
    });
  }

  persistProfileData(): void {
    let profileData: ProfileUpdateData = {
        userID: LogInComponent.userID,
        pathURL: LogInComponent.pathURL,
        fname: this.firstName,
        lname: this.lastName,
        year: ~~this.year, //converts to number and sets 0 if edge case
        gender: this.selectedGender,
        major: this.major,
        profilePic: this.paFile,
        backgroundPic: this.backgroundFile,
        interests: this.interest,
        courses: this.selectedCourses
    };
    this.databaseService.updateProfile(profileData).subscribe();
  }

 //edit button
  allowEdit(){
    this.signalContent = false;
  }

  allowSave(){
    this.signalContent = true;
    console.log(this.biography);
    this.databaseService.createAbout(LogInComponent.userID, this.biography).subscribe();
  }
}

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog-overview-example-dialog.html',
  styleUrls: ['./profileDialog.component.css']
})
export class DialogOverviewExampleDialog implements OnInit{
  //hard code list.. classes should be getting from the databases according to the major
  classCourses : string[] = [];//['CECS 324', 'CECS 225', 'CECS 328', 'CECS 343', 'CECS 451', 'CECS 453', 'd', 'd', 'd', 'f', 'fs', 'CECS 324', 'CECS 225', 'CECS 328', 'CECS 343', 'CECS 451', 'CECS 453', 'd', 'd', 'd', 'f', 'fs'];
  genderNames : string[] = ['MALE', 'FEMALE', 'NONBINARY', 'OTHER'];
  interestOptions: string[] = [];//['SPORTS','VIDEO GAMES','TRAVEL', 'ART', 'MUSIC', 'MOVIES','FOOD'];


  //data from interface DailogData is injected into the Dialog (the component that pops out)
  constructor(
    private databaseService: DatabaseService,
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  //inherits libraries from app root
  ngOnInit(): void {
    this.databaseService.getInterests().subscribe((data: string[]) => {
        this.interestOptions = data;
    });

    this.databaseService.getCourses().subscribe((data: string[]) => {
        this.classCourses = data;
    });
  }

  //main picture is uploaded and then displayed as the profile picture
  onFileSelected(event){
    const files = event.target.files;
    const reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.data.pa = reader.result;
    }
  }

  //background picture is uploaded and then displayed as the background picture
  backgroundChanged(event){
    const files = event.target.files;
    const reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.data.background = reader.result;
    }
  }


}
