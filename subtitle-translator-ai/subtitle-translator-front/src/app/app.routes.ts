import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home';
import { HelpComponent } from './components/help/help';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'help', component: HelpComponent },
  { path: '**', redirectTo: 'home' }
];