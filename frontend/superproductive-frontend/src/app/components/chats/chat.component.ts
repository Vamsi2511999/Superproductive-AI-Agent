import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';   // provides ngIf, ngFor, ngClass, pipes
import { FormsModule } from '@angular/forms';  

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  messages: {from: 'user'|'agent', text: string}[] = [];
  input = '';
  loading = false;

  constructor(private api: ApiService) {}

  send() {
    if (!this.input.trim()) return;
    const msg = this.input.trim();
    this.messages.push({from: 'user', text: msg});
    this.input = '';
    this.loading = true;
    this.api.chatQuery(msg).subscribe({
      next: (res) => {
        const reply = res?.reply || JSON.stringify(res);
        this.messages.push({from: 'agent', text: reply});
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.messages.push({from: 'agent', text: 'Error: Could not reach backend.'});
        this.loading = false;
      }
    });
  }
}