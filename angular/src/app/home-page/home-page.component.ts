import { Component, NgModule, OnInit } from '@angular/core';
import { Post } from '../api-objects/Post';
import { DatabaseService } from '../database.service';
import { About } from '../api-objects/About';
import { LogInComponent } from '../log-in/log-in.component';
import { Likes } from '../api-objects/Likes';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {
    firstName = "CONNECT LONG";
    lastName = "BEACH";
    //postText = "Here is a picture of the Walter Pyramid at the University of Long Beach.";
    privacy = "Public";
    currentDate = new Date();
    //likes = "12";

    uploadedFile? = "";
    postText = "";

    recentPosts: Post[] = [];
    postsLoaded: boolean = false;
    pictures = new Map();
    names = new Map();
    profilePics = new Map();
    likes = new Map();

    constructor(private databaseService: DatabaseService) { }
  
    ngOnInit(): void {
        this.currentDate.setUTCMilliseconds(1636601968);
        this.loadPosts();
    }

    loadPosts(): void {
        this.databaseService.getPosts(25).subscribe((data: Post[]) => {
            console.log(data);
            for(let post of data) {
                this.recentPosts.push(post);
                if (post.attachment !== 'null' && !this.pictures.has(post.attachment)) {
                    this.databaseService.getImage(post.attachment).subscribe(data => {
                        if(data.retrieved) {
                            this.pictures.set(post.attachment, data.image);
                        }
                    });
                }
                if(!this.names.has(post.author)){
                    this.databaseService.getName(~~post.author).subscribe(data => {
                        this.names.set(post.author, data.name);
                    });
                }
                if(!this.profilePics.has(post.author)) {
                    this.databaseService.getProfilePicture(~~post.author).subscribe(data => {
                        this.databaseService.getImage(data.name).subscribe(data => {
                            if(data.retrieved){
                                this.profilePics.set(post.author, data.image);
                            }
                        });
                    });
                }
                if(!this.likes.has(post.postID)) {
                    this.databaseService.getLikes(~~post.postID).subscribe(data => {
                        this.likes.set(post.postID, data.likes);
                    });
                }
            }
            console.log(this.recentPosts);
            this.postsLoaded = true;
        });
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
        if(this.postText.length > 0) {
            console.log(this.postText);
            if(this.uploadedFile === ""){
                this.databaseService.createPost(LogInComponent.userID, this.postText).subscribe(() => {
                    this.loadPosts();
                });
            }
            else{
                if(this.uploadedFile === undefined) {
                    this.uploadedFile = "";
                }
                this.databaseService.storeImage(this.uploadedFile).subscribe(data => {
                    this.databaseService.createPost(LogInComponent.userID, this.postText, data.path).subscribe(() => {
                        this.loadPosts();
                    });
                });
            }
            this.postText = '';
        }
    }

}