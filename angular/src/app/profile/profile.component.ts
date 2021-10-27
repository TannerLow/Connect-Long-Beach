import {Component, Inject, OnInit} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
//Data used for the Dialog data.. might want to export this interface to save space
export interface DialogData {
  major: string;
  year: string;
  gender: string;
  interest: string;
  courses: string;
  pa: string;
}


@Component({
  selector: 'profile-component',
  templateUrl: 'profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements  OnInit{

  major = ""
  year = ""
  gender = ""
  interest = ""
  courses = ""
  pa = "/static/assets/anonymous.png"
  constructor(public dialog: MatDialog) {}
  ngOnInit(): void {
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '30%',
      height: '70%',
      data: {major: this.major, year: this.year, gender: this.gender, interest: this.interest, courses: this.courses, pa: this.pa}
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.major = result[0];
      this.year = result[1];
      this.gender = result[2];
      this.interest = result[3];
      this.courses = result[4];
      console.log(this.major);
      console.log(this.year);
      console.log(this.gender);
      console.log(this.interest);
      console.log(this.courses);

    });
  }


}

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog-overview-example-dialog.html',
})
export class DialogOverviewExampleDialog implements OnInit{

  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  ngOnInit(): void {
  }

  onFileSelected(event){
    console.log(event);
  }

}
