import {Component, Input, OnInit} from '@angular/core';
import {Concept} from "../../../../shared/model/concept.class";

@Component({
  selector: 'app-concept-item',
  templateUrl: './concept-item.component.html',
  styleUrls: ['./concept-item.component.sass']
})
export class ConceptItemComponent implements OnInit {
  @Input()
  concept?: Concept;

  constructor() { }

  ngOnInit(): void {
  }

}
