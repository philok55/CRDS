void atom_string(t_atom *a, char *buf, unsigned int size)
{
    char tbuf[30];
    switch( a->a_type)
    {
        case A_SEMI: strcpy(buf, ";"); break;
        case A_COMMA: strcpy(buf, ","); break;
        case A_FLOAT:
            sprintf(tbuf, "%g", a->a_w.w_float);
            if (strlen(tbuf) < size-1) strcpy(buf, tbuf);
            else if (a->a_w.w_float < 0) strcpy(buf, "-");
            else strcat(buf, "+");
            break;
        case A_DOLLAR:
            sprintf(buf, "$%d", a->a_w.w_index);
            break;
        case A_DOLLSYM:
            sprintf(buf, "$%s", a->a_w.w_symbol->s_name);
            break;
        default:
            bug("atom_string");
    }
} 