// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { WelcomeComponent } from './welcome/welcome.component';
import { RagSystemComponent } from './rag-system/rag-system.component';

export const routes: Routes = [
  {
    path: '',
    component: WelcomeComponent
  },
  {
    path: 'rag-system',
    component: RagSystemComponent
  },
  {
    path: '**',
    redirectTo: ''
  }
];
