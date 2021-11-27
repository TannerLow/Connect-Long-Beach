import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable,of } from 'rxjs';
import {catchError,map,tap} from "rxjs/operators";
import { LoginCredentials } from './api-objects/LoginCredentials';
import { LoginResponse } from './api-objects/LoginResponse';
import { RegistrationInfo } from './api-objects/RegistrationInfo';
import { RegistrationResponse } from './api-objects/RegistrationResponse';
import { EmailCheckResponse } from './api-objects/EmailCheckResponse';
import sha256 from "fast-sha256";
import { Post } from './api-objects/Post';
import { CommentInfo } from './api-objects/CommentInfo';
import { Response } from './api-objects/Response';
import { PostInfo } from './api-objects/PostInfo';
import { PostResponse } from './api-objects/PostResponse';
import { ImageResponse } from './api-objects/ImageResponse';
import { StoreImageResponse } from './api-objects/StoreImageResponse';
import { StoreImageRequest } from './api-objects/StoreImageRequest';
import { About } from './api-objects/About';
import { AboutInfo } from './api-objects/AboutInfo';
import { LikePost } from './api-objects/LikePost';
import { Likes } from './api-objects/Likes';
import { ProfileData } from './api-objects/ProfileData';

const URL = 'api/';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

    constructor(
        private http: HttpClient
    ) { }

    login(credentials: LoginCredentials): Observable<LoginResponse> {
        return this.http.post<LoginResponse>(URL + "login", credentials)
            .pipe(
            tap(_ => console.log('login requested for ' + credentials.email)),
            catchError(this.handleError<LoginResponse>('login'))
        );
    }

    register(registrationInfo: RegistrationInfo): Observable<RegistrationResponse> {
        return this.http.post<RegistrationResponse>(URL + "register", registrationInfo)
            .pipe(
            tap(_ => console.log('registration requested for ' + registrationInfo.email)),
            catchError(this.handleError<RegistrationResponse>('register'))
        );
    }

    getProfile(pathURL: string): Observable<ProfileData> {
        return this.http.get<ProfileData>(URL + "getProfile/" + pathURL)
            .pipe(
            tap(_ => console.log('profile retrieved for url: ' + pathURL)),
            catchError(this.handleError<ProfileData>('getProfile'))
        );
    }

    isEmailInUse(email: string): Observable<EmailCheckResponse> {
        return this.http.get<EmailCheckResponse>(URL + "emailCheck/" + email)
            .pipe(
            tap(_ => console.log('email check for ' + email)),
            catchError(this.handleError<EmailCheckResponse>('isEmailInUse'))
        );
    }

    createPost(user_id: number, message: string): Observable<PostResponse> {
        let post: PostInfo = {
            userID: user_id,
            message: message
        } 
        return this.http.post<PostResponse>(URL + "post", post)
            .pipe(
                tap(_ => console.log('Posted with user id: ' + user_id)),
                catchError(this.handleError<PostResponse>('post'))
            );
    }

    getPosts(amount: number, user_id?: number): Observable<Post[]> {
        let path = URL + "getPosts/" + amount;
        if(user_id !== undefined) {
            path += "/" + user_id;
        }
        return this.http.get<Post[]>(path)
            .pipe(
                tap(_ => {
                    if(user_id === undefined) {
                        console.log('getting ' + amount + ' most recent posts');
                    }
                    else{
                        console.log('getting ' + amount + ' most recent posts from user with id ' + user_id)
                    }
                }),
                catchError(this.handleError<Post[]>('getPosts' + amount))
            );
    }

    createComment(user_id: number, post_id: number, message: string): Observable<Response> {
        let comment: CommentInfo = {
            postID: post_id,
            userID: user_id,
            message: message
        } 
        return this.http.post<Response>(URL + "comment", comment)
            .pipe(
                tap(_ => console.log('Posted a comment on post with user id: ' + user_id)),
                catchError(this.handleError<Response>('comment'))
            );
    }

    getComments(post_id: number): Observable<Post[]> {
        return this.http.get<Post[]>(URL + "getComments/" + post_id)
            .pipe(
                tap(_ => console.log('getting comments for post with id: ' + post_id)),
                catchError(this.handleError<Post[]>('getComments' + post_id))
            );
    }

    getImage(path: string): Observable<ImageResponse> {
        return this.http.get<ImageResponse>(URL + "getImage/" + path)
            .pipe(
                tap(_ => console.log('getting image from path: ' + path)),
                catchError(this.handleError<ImageResponse>('getImage ' + path))
            );
    }

    storeImage(imageData: string, path?: string): Observable<StoreImageResponse> {
        if(path === undefined) {
            path = "null"
        }

        let imageRequest: StoreImageRequest = {
            image: imageData,
            path: path
        }

        return this.http.post<StoreImageResponse>(URL + "storeImage", imageRequest)
            .pipe(
                tap(_ => console.log('Request to store image')),
                catchError(this.handleError<StoreImageResponse>('storeImage'))
            );
    }
    //TODO: come back and verify bottom is correct
    createAbout(user_id: number, message:string): Observable<Response>{
        let about: AboutInfo = {
            userID: user_id,
            aboutMe: message
        }
        return this.http.post<Response>(URL + "about", about)
        .pipe(
            tap(_=> console.log("Updated about me on profile with user id: " + user_id)),
            catchError(this.handleError<Response>('About'))
        );
    }


    likeUnlikePost(user_id: number, post_id:number): Observable<Response>{
        let like: LikePost = {
            userID: user_id,
            postID: post_id
        }
        return this.http.post<Response>(URL + "like",like)
        .pipe(
            tap(_=> console.log("Created like on post: " + post_id + " With user id: " + user_id)),
            catchError(this.handleError<Response>('Like'))
        );
    }

    getLikes(post_id: number): Observable<Likes[]>{
        return this.http.get<Likes[]>(URL + "getLikes/"+ post_id)
        .pipe(
          tap(_ => console.log("Getting amount of likes for post with id: " + post_id)),
          catchError(this.handleError<Likes[]>("getLikes" + post_id))  
        );
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {

            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead

            // TODO: better job of transforming error for user consumption
            console.log(`${operation} failed: ${error.message}`);

            // Let the app keep running by returning an empty result.
            return of(result as T);
        };
    }

    hashPassword(password: string): string {
        let encoder = new TextEncoder();
        let view = encoder.encode(password);
        view = sha256(view);
        return this.hexEncode(view);
    }

    private hexEncode(arr: Uint8Array){
        var hex;
        var result = "";

        arr.forEach( character => {
            //only use least significant 8 bits
            for(var i = 1; i >= 0; i--) {
                hex = (character >> (4 * i)) & 0xF;
                result += hex.toString(16);
            }
        });

        return result
    }
}
