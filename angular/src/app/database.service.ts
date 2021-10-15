import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable,of } from 'rxjs';
import {catchError,map,tap} from "rxjs/operators";
import { TableList } from './TableList';
import { LoginCredentials } from './api-objects/LoginCredentials';
import { LoginResponse } from './api-objects/LoginResponse';


const URL = 'api/';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

    constructor(
        private http: HttpClient
    ) { }

    retrieveTables(): Observable<TableList> {
        return this.http.get<TableList>(URL + "showTables")
            .pipe(
            tap(_ => console.log('fetched db table names')),
            catchError(this.handleError<TableList>('fetchTables'))
        );
    }

    login(credentials: LoginCredentials): Observable<LoginResponse> {
        console.log(credentials);
        return this.http.post<LoginResponse>(URL + "login", credentials)
            .pipe(
            tap(_ => console.log('login requested for ' + credentials.email)),
            catchError(this.handleError<LoginResponse>('login'))
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
}
