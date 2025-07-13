import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContextNoe } from './context-noe';

describe('ContextNoe', () => {
  let component: ContextNoe;
  let fixture: ComponentFixture<ContextNoe>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContextNoe]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContextNoe);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
