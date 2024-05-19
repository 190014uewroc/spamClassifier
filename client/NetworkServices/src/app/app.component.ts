import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {delay} from "rxjs";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = '';
  content = '';

  isLoading = false;
  classificationResult = '';

  readonly HAM = 'ham';
  readonly SPAM = 'spam';
  private readonly toastrTitle = 'E-mail classification result';
  constructor(private http: HttpClient, private toastr: ToastrService) {

  }

  predict() {
    this.isLoading = true;
    this.http.post('http://localhost:5000/predict', {content: [this.title, this.content].join(` `)}).pipe(delay(500)).subscribe((res: any) => {
        this.classificationResult = res?.[0]?.content;
        if (this.classificationResult === this.HAM) {
          this.toastr.info(res?.[0]?.content, this.toastrTitle);
        } else {
          this.toastr.error(res?.[0]?.content, this.toastrTitle);
        }
        this.isLoading = false;
        setTimeout(()=> {
          this.classificationResult = '';
        }, 1000);
      }
    );
  }
}
