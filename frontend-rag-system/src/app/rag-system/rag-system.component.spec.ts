import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RagSystemComponent } from './rag-system.component';

describe('RagSystemComponent', () => {
  let component: RagSystemComponent;
  let fixture: ComponentFixture<RagSystemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RagSystemComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RagSystemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
