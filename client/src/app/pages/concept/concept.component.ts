import {Component, OnInit} from '@angular/core';
import {ConceptService} from "../../shared/services/concept.service";
import {Concept} from "../../shared/model/concept.class";
import {suppressDefaultBehaviour} from "../../shared/utils";

@Component({
  selector: 'app-concept',
  templateUrl: './concept.component.html',
  styleUrls: ['./concept.component.sass']
})
export class ConceptComponent implements OnInit {
  concepts: Concept[] = [];
  selectedConcept: Concept | undefined;

  constructor(private conceptService: ConceptService) {
  }

  ngOnInit(): void {
    this.conceptService.listConcept().subscribe(concepts => this.concepts = concepts);
  }

  onSelect(concept: Concept) {
    this.selectedConcept = concept;
  }

  onDelete(concept: Concept, event: MouseEvent) {
    suppressDefaultBehaviour(event);
    console.log('Delete', concept)
  }
}
