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

    getPosts(amount: number): Observable<Post[]> {
        return this.http.get<Post[]>(URL + "getPosts/" + amount)
            .pipe(
                tap(_ => console.log('getting ' + amount + ' most recent posts')),
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
