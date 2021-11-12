import { Component } from '@angular/core';
import { DatabaseService } from './database.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})

export class AppComponent {
    title = 'angular';

    password = "";

    constructor(private databaseService: DatabaseService) {}

    ngOnInit() {
        //this.post_test();
        this.getPosts_test();
        //this.comment_test();
        this.getComments_test();
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
}
