import { MapPin, Phone, Sparkles } from "lucide-react";

export default function ContactPage() {
  return (
    <div className="mx-auto max-w-7xl px-6 py-10 md:px-10 lg:px-16" data-testid="contact-page">
      <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
        <section className="rounded-[36px] border border-white/10 bg-[linear-gradient(145deg,_rgba(13,24,53,0.98),_rgba(10,18,38,0.92))] p-8 text-[#fdfbf7] md:p-10" data-testid="contact-intro-card">
          <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="contact-eyebrow">Visit Royal Spark</p>
          <h1 className="mt-5 font-display text-5xl leading-none" data-testid="contact-heading">Private jewelry consultations in Houston.</h1>
          <p className="mt-6 max-w-lg text-sm leading-relaxed text-white/76" data-testid="contact-description">
            Speak with us about rings, bangles, grillz, charms, earrings, bracelets, and custom luxury requests. We’re available for showroom-style guidance and direct client support.
          </p>
          <div className="mt-10 space-y-4 text-sm text-white/78">
            <div className="flex items-start gap-3 rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid="contact-address-card">
              <MapPin className="mt-0.5 h-5 w-5 text-[#d8b85d]" />
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]">Address</p>
                <p className="mt-1" data-testid="contact-address-text">100 Sharpstown Center #2090, Houston, TX 77036, USA</p>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid="contact-phone-card">
              <Phone className="mt-0.5 h-5 w-5 text-[#d8b85d]" />
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-[#d8b85d]">Phone</p>
                <p className="mt-1" data-testid="contact-phone-text">+1 832 329 7145</p>
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[36px] border border-white/10 bg-[#111d3a]/90 p-8 md:p-10" data-testid="contact-services-card">
          <p className="text-xs uppercase tracking-[0.32em] text-[#d8b85d]" data-testid="contact-services-eyebrow">Category support</p>
          <h2 className="mt-4 font-display text-4xl text-white" data-testid="contact-services-heading">What clients can inquire about</h2>
          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            {[
              "Chains",
              "Bangles",
              "Grillz",
              "Charms",
              "Rings",
              "Earrings",
              "Bracelets",
            ].map((item) => (
              <div key={item} className="rounded-[24px] border border-white/10 bg-white/5 p-4" data-testid={`contact-category-${item.toLowerCase()}`}>
                <div className="flex items-center gap-2 text-[#d8b85d]">
                  <Sparkles className="h-4 w-4" />
                  <p className="text-xs uppercase tracking-[0.22em]">{item}</p>
                </div>
                <p className="mt-3 text-sm text-[#cbd2ec]">Available for purchase guidance, custom requests, and future Shopify product consultation.</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}