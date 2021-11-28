import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailCreationComponent } from './email-creation.component';

describe('EmailCreationComponent', () => {
  let component: EmailCreationComponent;
  let fixture: ComponentFixture<EmailCreationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EmailCreationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EmailCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
