import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, MatCardModule, MatInputModule, MatButtonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  password = '';
  constructor(private http: HttpClient, private router: Router) {}
  login() {
    this.http.post<{token:string}>('http://192.168.0.6:5000/api/login', {password: this.password})
      .subscribe(res => {
        localStorage.setItem('token', res.token);
        this.router.navigate(['/translator']);
      });
  }
}
