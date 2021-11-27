import { Component } from '@angular/core';
import { LogInComponent } from './log-in/log-in.component';
import { DatabaseService } from './database.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})

export class AppComponent {
    title = 'angular';

    password = "";

    image = "static/assets/logo.png";

    constructor(private databaseService: DatabaseService) {}

    ngOnInit() {
        //this.post_test();
        this.getPosts_test();
        //this.comment_test();
        this.getComments_test();
        //this.storeImage_test();
        this.getImage_test();
        //this.about_test();
        //this.like_test();
        this.getLikes_test();
    }

    // test to show cross component variables, specifically user ID
    getUID() {
        if(LogInComponent.loggedIn){
            console.log("user id from retrieval: " + LogInComponent.userID);
        }
        else {
            console.log("user not logged in")
        }
        return LogInComponent.userID;
    }

    getPosts_test(): void {
        this.databaseService.getPosts(5, 22).subscribe(data => {
            console.log(data);
        });
    }

    getComments_test(): void {
        this.databaseService.getComments(51).subscribe(data => {
            console.log(data);
        });
    }

    comment_test(): void {
        this.databaseService.createComment(22, 51, "An original comment.").subscribe(data => {
            console.log("Comment posted: " + data.response);
        });
    }

    post_test(): void {
        this.databaseService.createPost(22, "This is a test of the post system.").subscribe(data => {
            console.log("New post id: " + data.postID);
        });
    }

    getImage_test(): void {
        this.databaseService.getImage("wd0abw7c7l").subscribe(data => {
            console.log(data);
            this.image = data.image;
        });
    }

    storeImage_test(): void {
        this.databaseService.storeImage("imagine this is image data", "wd0abw7c7l").subscribe(data => {
            console.log(data);
        });
    }

    getProfile_test(): void {
        this.databaseService.getProfile("gsjfrudrab").subscribe(data => {
            console.log(data);
        });
    }
    about_test(): void{
        this.databaseService.createAbout(1,"Mayor of Sardignia!_").subscribe(data => {
            console.log("about created: " + data.response);
        });
    }

    like_test(): void{
        this.databaseService.likeUnlikePost(1,65).subscribe(data => {
            console.log("like created: " + data.response);
        });
    }

    getLikes_test(): void{
        this.databaseService.getLikes(65).subscribe(data => {
            console.log(data);
        });
    }

}
