import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/components/ui/sonner";
import { submitBespokeInquiry } from "@/lib/api";

const initialForm = {
  name: "",
  email: "",
  jewelry_type: "Custom Ring",
  budget: "2,000 - 5,000",
  material_preference: "18K Gold",
  inspiration: "",
  timeline: "Within 1-2 months",
  message: "",
};

export default function BespokePage() {
  const [form, setForm] = useState(initialForm);
  const mutation = useMutation({
    mutationFn: submitBespokeInquiry,
    onSuccess: () => {
      toast.success("Your bespoke request has been received.");
      setForm(initialForm);
    },
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    mutation.mutate(form);
  };

  return (
    <div className="mx-auto max-w-7xl px-6 py-10 md:px-10 lg:px-16" data-testid="bespoke-page">
      <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
        <section className="rounded-[36px] bg-[#0a0a0a] p-8 text-[#fdfbf7] md:p-10" data-testid="bespoke-intro-card">
          <p className="text-xs uppercase tracking-[0.32em] text-[#c5a059]" data-testid="bespoke-eyebrow">Custom jewelry</p>
          <h1 className="mt-5 font-display text-5xl leading-none" data-testid="bespoke-heading">Create a piece with your own signature.</h1>
          <p className="mt-6 max-w-lg text-sm leading-relaxed text-white/76" data-testid="bespoke-description">
            Share your budget, material preference, timeline, and inspiration. This flow is already prepared for future Shopify-linked customer intake.
          </p>
          <div className="mt-10 space-y-4 text-sm text-white/78">
            <div className="rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid="bespoke-step-1">1. Tell us the type of piece you want.</div>
            <div className="rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid="bespoke-step-2">2. Choose budget and preferred materials.</div>
            <div className="rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid="bespoke-step-3">3. Receive a concierge reply with next steps.</div>
          </div>
        </section>

        <section className="rounded-[36px] border border-[#ece4d8] bg-white/90 p-8 md:p-10" data-testid="bespoke-form-card">
          <form className="grid gap-6" onSubmit={handleSubmit} data-testid="bespoke-form">
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-name">Name</label>
                <Input id="bespoke-name" name="name" value={form.name} onChange={handleChange} className="mt-3 h-12 rounded-none border-0 border-b border-[#cab995] px-0 shadow-none focus-visible:ring-0" data-testid="bespoke-name-input" required />
              </div>
              <div>
                <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-email">Email</label>
                <Input id="bespoke-email" type="email" name="email" value={form.email} onChange={handleChange} className="mt-3 h-12 rounded-none border-0 border-b border-[#cab995] px-0 shadow-none focus-visible:ring-0" data-testid="bespoke-email-input" required />
              </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-type">Jewelry type</label>
                <Input id="bespoke-type" name="jewelry_type" value={form.jewelry_type} onChange={handleChange} className="mt-3 h-12 rounded-none border-0 border-b border-[#cab995] px-0 shadow-none focus-visible:ring-0" data-testid="bespoke-type-input" required />
              </div>
              <div>
                <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-budget">Budget</label>
                <Input id="bespoke-budget" name="budget" value={form.budget} onChange={handleChange} className="mt-3 h-12 rounded-none border-0 border-b border-[#cab995] px-0 shadow-none focus-visible:ring-0" data-testid="bespoke-budget-input" required />
              </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-material">Material preference</label>
                <Input id="bespoke-material" name="material_preference" value={form.material_preference} onChange={handleChange} className="mt-3 h-12 rounded-none border-0 border-b border-[#cab995] px-0 shadow-none focus-visible:ring-0" data-testid="bespoke-material-input" required />
              </div>
              <div>
                <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-timeline">Timeline</label>
                <Input id="bespoke-timeline" name="timeline" value={form.timeline} onChange={handleChange} className="mt-3 h-12 rounded-none border-0 border-b border-[#cab995] px-0 shadow-none focus-visible:ring-0" data-testid="bespoke-timeline-input" required />
              </div>
            </div>

            <div>
              <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-inspiration">Inspiration link</label>
              <Input id="bespoke-inspiration" name="inspiration" value={form.inspiration} onChange={handleChange} className="mt-3 h-12 rounded-none border-0 border-b border-[#cab995] px-0 shadow-none focus-visible:ring-0" data-testid="bespoke-inspiration-input" />
            </div>

            <div>
              <label className="text-xs uppercase tracking-[0.24em] text-[#666666]" htmlFor="bespoke-message">Tell us about the piece</label>
              <Textarea id="bespoke-message" name="message" value={form.message} onChange={handleChange} className="mt-3 min-h-[140px] rounded-[24px] border-[#e7e1d7] bg-[#fbf7f1]" data-testid="bespoke-message-input" required />
            </div>

            <Button type="submit" className="h-12 rounded-full bg-[#022b22] px-6 text-white hover:bg-[#0a0a0a]" data-testid="bespoke-submit-button" disabled={mutation.isPending}>
              {mutation.isPending ? "Sending request…" : "Send bespoke request"}
            </Button>
          </form>
        </section>
      </div>
    </div>
  );
}
