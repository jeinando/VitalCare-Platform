# C4 container view

The Backend API is the single gateway to data: the four front ends never touch PostgreSQL, Blob Storage or Key Vault directly.

```mermaid
flowchart TB
    client([Client and patient])
    caregiver([Caregiver])
    admin([Provider admin])

    subgraph frontends[Front ends]
        public["Public site<br/>Next.js on Vercel<br/>vitalcarecr.com"]
        portal["Client portal<br/>Next.js on Azure<br/>app.vitalcarecr.com"]
        mobile["Mobile app<br/>Flutter, client and caregiver roles"]
        adminpanel["Admin panel<br/>Next.js on Azure, MFA required<br/>admin.vitalcarecr.com"]
    end

    api["Backend API<br/>ASP.NET Core modular monolith<br/>Azure App Service · api.vitalcarecr.com"]

    subgraph data[Data stores on Azure]
        db[("PostgreSQL<br/>Azure Flexible Server<br/>patients, bookings, audit log")]
        blob[("Blob Storage<br/>payment receipts, quote PDFs")]
        kv[("Key Vault<br/>secrets, encryption keys")]
    end

    fcm["Firebase Cloud Messaging"]:::external

    client --> public
    client --> portal
    client --> mobile
    caregiver --> mobile
    admin --> adminpanel

    public -- "HTTPS / JSON / JWT" --> api
    portal --> api
    mobile --> api
    adminpanel --> api

    api --> db
    api --> blob
    api --> kv
    api --> fcm

    classDef external stroke-dasharray: 4 3
```

Related decisions: [ADR-001](../adr/0001-backend-aspnet-core-modular-monolith.md), [ADR-002](../adr/0002-postgresql-primary-database.md), [ADR-003](../adr/0003-single-flutter-app-with-roles.md), [ADR-008](../adr/0008-react-nextjs-portal-and-admin.md), [ADR-007](../adr/0007-azure-cloud-provider.md).
