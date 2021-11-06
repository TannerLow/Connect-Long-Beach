import {Component, Inject, OnInit} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
//Data used for the Dialog data.. might want to export this interface to save space
export interface DialogData {
  firstName: string;
  lastName: string;
  major: string;
  year: string;
  selectedGender: string [];
  interest: string;
  selectedCourses: string [];
  pa: any;
  url: any;
}


@Component({
  selector: 'profile-component',
  templateUrl: 'profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements  OnInit{
  firstName = ""
  lastName = ""
  major = ""
  year = ""
  selectedGender = [];
  interest = ""
  selectedCourses = [];
  pa = "/static/assets/anonymous.png"
  constructor(public dialog: MatDialog) {}
  ngOnInit(): void {
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '30%',
      data: {firstName: this.firstName, lastName: this.lastName,major: this.major, year: this.year, selectedGender: this.selectedGender, interest: this.interest, selectedCourses: this.selectedCourses, pa: this.pa}
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      console.log(result)
      this.firstName = result[0];
      this.lastName = result[1];
      this.major = result[2];
      this.year = result[3];
      this.selectedGender = result[4];
      this.interest = result[5];
      this.selectedCourses = result[6];
      this.pa = result[7];
      console.log(this.firstName);
      console.log(this.lastName);
      console.log(this.major);
      console.log(this.year);
      console.log(this.selectedGender);
      console.log(this.interest);
      console.log(this.selectedCourses);

    });
  }

}

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog-overview-example-dialog.html',
  styleUrls: ['./profile.component.css']
})
export class DialogOverviewExampleDialog implements OnInit{
  classCourses : string[] = ['CECS 324', 'CECS 225', 'CECS 328', 'CECS 343', 'CECS 451', 'CECS 453'];
  genderNames : string[] = ['MALE', 'FEMALE', 'LESBIAN', 'GAY', 'HETEROSEXUAL', 'BISEXUAL'];


  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  ngOnInit(): void {
  }

  onFileSelected(event){
    const files = event.target.files;
    const reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.data.pa = reader.result;
    }
  }


}
