import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule, routingComponents} from './app-routing.module';
import { AppComponent } from './app.component';

import { FormsModule } from '@angular/forms';
import { LogInComponent } from './log-in/log-in.component';

import {HttpClientModule} from "@angular/common/http";

import { ValidateEqualModule } from  'ng-validate-equal';
import { SignUpComponent } from './sign-up/sign-up.component';

@NgModule({
  declarations: [
    AppComponent,
    routingComponents,
    LogInComponent,
    SignUpComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    ValidateEqualModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
