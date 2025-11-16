import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Task } from '../../models/task.model';
import { DatePipe } from '@angular/common';
import { CommonModule } from '@angular/common';   // provides ngIf, ngFor, ngClass, pipes
import { FormsModule } from '@angular/forms';  


@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [ DatePipe, CommonModule, FormsModule],
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];
  filtered: Task[] = [];
  loading = false;
  filterPriority: string = 'All';
  fromDate: string = '';
  toDate: string = '';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadTasks();
  }

  loadTasks() {
    this.loading = true;
    this.api.getTasks().subscribe({
      next: (res) => { this.tasks = res; this.applyFilters(); this.loading = false; },
      error: (err) => { console.error(err); this.loading = false; }
    });
  }

  applyFilters() {
    this.filtered = this.tasks.filter(t => {
      if (this.filterPriority !== 'All' && t.priority !== this.filterPriority) return false;
      if (this.fromDate && t.eta) {
        if (new Date(t.eta) < new Date(this.fromDate)) return false;
      }
      if (this.toDate && t.eta) {
        if (new Date(t.eta) > new Date(this.toDate)) return false;
      }
      return true;
    });
  }

  markDone(t: Task) {
    t.status = 'Done';
    // optionally persist to backend (skipped in MVP) - call API here
  }

}