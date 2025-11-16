// src/main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';        // if you use HttpClienth                // if you have routing
import { App } from './app/app';                                     // root standalone component

bootstrapApplication(App, {
  providers: [
    provideHttpClient(),   // remove if you don't use HttpClient
    // provideRouter([...]) // add router providers if you use routing
  ]
}).catch(err => console.error(err));
