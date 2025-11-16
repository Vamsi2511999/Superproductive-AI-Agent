// src/app/app.ts
import { Component } from '@angular/core';
import { TaskListComponent } from './components/task-list/task-list.component';
import { ChatComponent } from './components/chats/chat.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, TaskListComponent, ChatComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  title = 'Superproductive AI Agent - Demo';
}
