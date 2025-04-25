
// src/app/rag-system/rag-system.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

// Angular Material
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTooltipModule } from '@angular/material/tooltip';

// Service
import { RagService } from '../services/rag.service';

interface ChatMessage {
  isUser: boolean;
  text: string;
  timestamp: Date;
  sources?: any[];
}

@Component({
  selector: 'app-rag-system',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatDividerModule,
    MatListModule,
    MatExpansionModule,
    MatTooltipModule
  ],
  templateUrl: './rag-system.component.html',
  styleUrls: ['./rag-system.component.css']
})
export class RagSystemComponent {
  queryForm: FormGroup;
  messages: ChatMessage[] = [];
  isProcessing = false;
  isUploading = false;
  isRebuildingIndex = false;
  uploadProgress = 0;
  selectedFile: File | null = null;

  constructor(
    private fb: FormBuilder,
    private ragService: RagService,
    private snackBar: MatSnackBar
  ) {
    this.queryForm = this.fb.group({
      query: ['', Validators.required]
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files?.length) {
      const file = input.files[0];

      if (this.isValidFileType(file)) {
        this.selectedFile = file;
      } else {
        this.snackBar.open('Please select a PDF file', 'Close', { duration: 3000 });
        this.selectedFile = null;
      }
    }
  }

  isValidFileType(file: File): boolean {
    return file.type === 'application/pdf';
  }

  uploadFile(): void {
    if (!this.selectedFile || this.isUploading) return;

    this.isUploading = true;
    this.uploadProgress = 0;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    // Simulate upload progress
    const interval = setInterval(() => {
      this.uploadProgress += 5;
      if (this.uploadProgress >= 100) {
        clearInterval(interval);
      }
    }, 100);

    this.ragService.uploadDocument(formData).subscribe({
      next: (response) => {
        clearInterval(interval);
        this.uploadProgress = 100;
        this.isUploading = false;
        this.snackBar.open(`Uploaded ${response.name} with ${response.chunk_count} chunks`, 'Close', { duration: 5000 });
        this.selectedFile = null;
      },
      error: (error) => {
        clearInterval(interval);
        this.isUploading = false;
        this.uploadProgress = 0;
        console.error('Upload error:', error);
        this.snackBar.open('Error uploading document', 'Close', { duration: 3000 });
      }
    });
  }

  rebuildIndex(): void {
    if (this.isRebuildingIndex) return;

    this.isRebuildingIndex = true;
    this.snackBar.open('Rebuilding index...', 'Close', { duration: 3000 });

    this.ragService.rebuildIndex().subscribe({
      next: (response) => {
        this.isRebuildingIndex = false;
        this.snackBar.open(`Index rebuilt! Processed ${response.documents_processed} documents with ${response.total_chunks} chunks`, 'Close', { duration: 5000 });
      },
      error: (error) => {
        this.isRebuildingIndex = false;
        console.error('Error rebuilding index:', error);
        this.snackBar.open('Error rebuilding index', 'Close', { duration: 3000 });
      }
    });
  }

  sendQuery(): void {
    if (this.queryForm.invalid || this.isProcessing) return;

    const queryText = this.queryForm.get('query')?.value;

    // Add user message
    this.messages.push({
      isUser: true,
      text: queryText,
      timestamp: new Date()
    });

    // Reset form
    this.queryForm.reset();

    // Show processing
    this.isProcessing = true;

    // Scroll to bottom
    setTimeout(() => this.scrollToBottom(), 50);

    // Send query to API
    this.ragService.query(queryText).subscribe({
      next: (response) => {
        // Add AI response
        this.messages.push({
          isUser: false,
          text: response.answer,
          timestamp: new Date(),
          sources: response.sources
        });

        this.isProcessing = false;

        // Scroll to bottom
        setTimeout(() => this.scrollToBottom(), 100);
      },
      error: (error) => {
        console.error('Error querying:', error);

        // Add error message
        this.messages.push({
          isUser: false,
          text: 'Sorry, I encountered an error processing your query.',
          timestamp: new Date()
        });

        this.isProcessing = false;

        // Scroll to bottom
        setTimeout(() => this.scrollToBottom(), 100);
      }
    });
  }

  clearChat(): void {
    this.messages = [];
  }

  private scrollToBottom(): void {
    const chatContainer = document.querySelector('.chat-messages');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }
}
