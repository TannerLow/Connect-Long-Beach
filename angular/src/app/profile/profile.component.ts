import {Component, Inject, OnInit} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from "@angular/material/dialog";
export interface DialogData{
  major: string;
  year: string;
  gender: string;
  interest: string;
  courses: string;
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  major = ""
  year = ""
  gender = ""
  interest = ""
  courses = ""
  constructor() { }

  ngOnInit(): void {
  }

  openInformation(): void{
    // const dialogRed = this.dialog.open(DialogOverview,{
    //   width: '250px',
    //   data: {major: this.major, year: this.year, gender: this.gender, interest: this.interest, courses: this.courses}
    // });
  }

}

// @Component({
//   selector: 'profile-dialog-overview',
//   templateUrl: 'profile-dialog-overview.html'
// })
// export class DialogOverview implements OnInit{
//   constructor(
//     public dialogRef:  MatDialogRef<DialogOverview>,
//     @Inject(MAT_DIALOG_DATA) public data: DialogData){}
//
//     ngOnInit(): void {
//     }
//     onDone(): void{
//       this.dialogRef.close();
//     }
// }
