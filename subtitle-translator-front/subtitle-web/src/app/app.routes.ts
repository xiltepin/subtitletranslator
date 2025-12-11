import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { TranslatorComponent } from './translator/translator.component';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'translator', component: TranslatorComponent }
];
