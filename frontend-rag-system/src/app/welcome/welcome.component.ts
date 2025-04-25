// src/app/welcome/welcome.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatCardModule],
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.css']
})
export class WelcomeComponent implements OnInit {
  fullText = 'Welcome to PDF Question Answering System';
  displayText = '';
  isTyping = false;
  typingSpeed = 100;

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.typeText();
  }

  typeText(): void {
    this.isTyping = true;
    let i = 0;

    const typeInterval = setInterval(() => {
      if (i < this.fullText.length) {
        this.displayText += this.fullText.charAt(i);
        i++;
      } else {
        clearInterval(typeInterval);
        this.isTyping = false;
      }
    }, this.typingSpeed);
  }

  navigateToRagSystem(): void {
    this.router.navigate(['/rag-system']);
  }
}
