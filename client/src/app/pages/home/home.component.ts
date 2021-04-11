import { Component, OnInit } from '@angular/core';
import {Concept} from "../../shared/model/concept.class";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.sass']
})
export class HomeComponent implements OnInit {
  concepts: Concept[] = [];

  constructor() { }

  ngOnInit(): void {
  }

}
