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
        this.getPosts_test();
    }

    getPosts_test(): void {
        this.databaseService.getPosts(5).subscribe(data => {
            console.log(data);
        });
    }
}
